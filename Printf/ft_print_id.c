/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_id.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/18 22:20:39 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/30 21:17:08 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_print_nbr(int n)
{
	int	len;

	len = 0;
	if (n == -2147483648)
	{
		ft_putstr_fd("-2147483648", 1);
		return (11);
	}
	if (n < 0)
	{
		len += ft_print_char('-');
		n = -n;
	}
	if (n > 9)
	{
		len += ft_print_nbr(n / 10);
		len += ft_print_nbr(n % 10);
	}
	else
		len += ft_print_char(n + '0');
	return (len);
}
