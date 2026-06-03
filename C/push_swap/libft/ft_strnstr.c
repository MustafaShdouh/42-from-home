/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/10 19:36:30 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/30 20:23:33 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
//#include <stddef.h>
//#include <string.h>
#include "libft.h"

char	*ft_strnstr(const char *big, const char *little, size_t len)
{
	size_t	b;
	size_t	l;

	b = 0;
	if (!*little)
		return ((char *)big);
	while (b < len && big[b])
	{
		l = 0;
		while ((big[b + l] == little[l]) && ((b + l) < len))
		{
			if (little[l + 1] == '\0')
				return ((char *)&big[b]);
			l++;
		}
		b++;
	}
	return (NULL);
}

/*int	main(void)
{
	const char *largestring = "Foo Bar Baz";
             const char *smallstring = "Baz";
             char *ptr;

             ptr = ft_strnstr(largestring, smallstring, 11);
	     printf("the function returned: %s\n", ptr);
}*/
