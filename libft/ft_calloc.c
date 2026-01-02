/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/10 20:37:58 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/30 20:47:26 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stddef.h>
//#include <stdio.h>
//#include <stdint.h>
//#include <stdlib.h>
#include "libft.h"

void	*ft_calloc(size_t nmemb, size_t size)
{
	void	*ptr;
	size_t	total_size;

	if ((nmemb != 0) && (size > (4294967295 / nmemb)))
		return (NULL);
	total_size = nmemb * size;
	ptr = malloc(total_size);
	if (!ptr)
		return (NULL);
	ft_bzero(ptr, total_size);
	return (ptr);
}

/*int	main(void)
{
	size_t	nmemb = 439265692367;
	size_t	i;
	int		*arr;

	arr = (int *)ft_calloc(nmemb, sizeof(int));
	if (!arr)
		printf("Failed");
	i = 0;
	while (i < nmemb)
	{
		printf("Index %zu: %d ", i, arr[i]);
		if (arr[i] != 0)
			printf("Error");
		i++;
	}
}*/
