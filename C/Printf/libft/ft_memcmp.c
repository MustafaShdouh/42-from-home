/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcmp.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/09 21:29:56 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/30 20:00:51 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
//#include <string.h>
//#include <stddef.h>
#include "libft.h"

int	ft_memcmp(const void *s1, const void *s2, size_t n)
{
	size_t				i;
	const unsigned char	*ptr1;
	const unsigned char	*ptr2;

	if (n == 0)
		return (0);
	i = 0;
	ptr1 = (const unsigned char *)s1;
	ptr2 = (const unsigned char *)s2;
	while (i < n)
	{
		if (ptr1[i] != ptr2[i])
			return (ptr1[i] - ptr2[i]);
		i++;
	}
	return (0);
}

/*int	main(void)
{
	int	cmp;
	
	cmp = ft_memcmp("888","1", 2);
	printf("%d\n", cmp);
	cmp = memcmp("888","1", 2); // this will give a different 
	// number but will be pos or neg
        printf("%d\n", cmp);
}*/
